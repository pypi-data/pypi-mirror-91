import torch
import torch.nn.functional as F
from torch import nn, einsum

class GVP(nn.Module):
    def __init__(
        self,
        *,
        dim_coors_in,
        dim_feats_in,
        dim_feats_out,
        dim_coors_out,
        feats_activation = nn.Sigmoid(),
        coors_activation = nn.Sigmoid()
    ):
        super().__init__()
        self.dim_coors_in = dim_coors_in
        self.dim_feats_in = dim_feats_in

        self.dim_coors_out = dim_coors_out
        dim_h = max(dim_coors_in, dim_coors_out)

        self.Wh = nn.Parameter(torch.randn(dim_coors_in, dim_h))
        self.Wu = nn.Parameter(torch.randn(dim_h, dim_coors_out))

        self.coors_activation = coors_activation

        self.to_feats_out = nn.Sequential(
            nn.Linear(dim_h + dim_feats_in, dim_feats_out),
            feats_activation
        )

    def forward(self, feats, coors):
        b, n, _, v, c = *feats.shape, *coors.shape

        assert c == 3 and v == self.dim_coors_in, 'coordinates have wrong dimensions'
        assert n == self.dim_feats_in, 'scalar features have wrong dimensions'

        Vh = einsum('b v c, v h -> b h c', coors, self.Wh)
        Vu = einsum('b h c, h u -> b u c', Vh, self.Wu)

        sh = torch.norm(Vh, p = 2, dim = -1)
        vu = torch.norm(Vu, p = 2, dim = -1, keepdim = True)

        s = torch.cat((feats, sh), dim = 1)

        feats_out = self.to_feats_out(s)
        coors_out = self.coors_activation(vu) * Vu

        return feats_out, coors_out
