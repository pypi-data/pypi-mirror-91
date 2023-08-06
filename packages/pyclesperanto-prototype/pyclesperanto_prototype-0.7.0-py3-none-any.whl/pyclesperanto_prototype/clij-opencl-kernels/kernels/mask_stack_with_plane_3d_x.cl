__constant sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;

__kernel void mask_stack_with_plane_3d(
    IMAGE_src_TYPE  src,
    IMAGE_mask_TYPE  mask,
    IMAGE_dst_TYPE dst
)
{
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  const int z = get_global_id(2);

  const int4 pos3d = (int4){x,y,z,0};
  const int2 pos2d = (int2){x,y};

  IMAGE_src_PIXEL_TYPE value = 0;
  if (READ_mask_IMAGE(mask, sampler, pos2d).x != 0) {
    value = READ_src_IMAGE(src, sampler, pos3d).x;
  }

  WRITE_dst_IMAGE (dst, pos3d, CONVERT_dst_PIXEL_TYPE(value));
}
