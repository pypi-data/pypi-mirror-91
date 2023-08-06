__constant sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;

__kernel void maximum_image_and_scalar_2d(
    IMAGE_src_TYPE  src,
    IMAGE_dst_TYPE  dst,
    float valueB
)
{
  const int x = get_global_id(0);
  const int y = get_global_id(1);

  const int2 pos = (int2){x,y};

  const float input = READ_src_IMAGE(src, sampler, pos).x;
  const float input1 = valueB;

  const IMAGE_dst_PIXEL_TYPE value = CONVERT_dst_PIXEL_TYPE(max(input, input1));

  WRITE_dst_IMAGE(dst, pos, value);
}
