__constant sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;

__kernel void mean_slice_by_slice_sphere_3d
(
  IMAGE_dst_TYPE dst,
  IMAGE_src_TYPE src,
  const int Nx,
  const int Ny
)
{
  const int i = get_global_id(0);
  const int j = get_global_id(1);
  const int k = get_global_id(2);
  const int4 coord = (int4){i,j,k,0};

  const int4   e = (int4)  {(Nx-1)/2, (Ny-1)/2, 0, 0 };

  float aSquared = e.x * e.x;
  float bSquared = e.y * e.y;
    if (aSquared == 0) {
        aSquared = FLT_MIN;
    }
    if (bSquared == 0) {
        bSquared = FLT_MIN;
    }

  float sum = 0;
  int count = 0;

  for (int x = -e.x; x <= e.x; x++) {
    float xSquared = x * x;
    for (int y = -e.y; y <= e.y; y++) {
      float ySquared = y * y;
      if (xSquared / aSquared + ySquared / bSquared <= 1.0) {
        sum = sum + READ_src_IMAGE(src,sampler,coord+((int4){x,y,0,0})).x;
        count++;
      }
    }
  }

  IMAGE_dst_PIXEL_TYPE res = CONVERT_dst_PIXEL_TYPE(sum / count);
  WRITE_dst_IMAGE(dst, coord, res);
}
