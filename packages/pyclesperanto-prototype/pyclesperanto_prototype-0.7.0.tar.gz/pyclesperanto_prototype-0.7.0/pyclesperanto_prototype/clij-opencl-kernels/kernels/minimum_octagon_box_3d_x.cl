__constant sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;

__kernel void minimum_octagon_box_3d
(
  IMAGE_dst_TYPE dst, IMAGE_src_TYPE src
)
{
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  const int z = get_global_id(2);

  const int4 pos = (int4){x,y,z,0};

  float minimum = READ_src_IMAGE(src, sampler, pos).x;
  for (int ax = -1; ax <= 1; ax++) {
    for (int ay = -1; ay <= 1; ay++) {
      for (int az = -1; az <= 1; az++) {
        float value = READ_src_IMAGE(src, sampler, (pos + (int4){ax, ay, az, 0})).x;
        if (minimum > value) {
          minimum = value;
        }
      }
    }
  }
  WRITE_dst_IMAGE (dst, pos, CONVERT_dst_PIXEL_TYPE(minimum));
}

