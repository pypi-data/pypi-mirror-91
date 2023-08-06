__constant sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;

__kernel void maximum_images_2d(
    IMAGE_src_TYPE  src,
    IMAGE_src1_TYPE  src1,
    IMAGE_dst_TYPE  dst
)
{
  const int x = get_global_id(0);
  const int y = get_global_id(1);

  const int2 pos = (int2){x,y};

  const IMAGE_src_PIXEL_TYPE input = READ_src_IMAGE(src, sampler, pos).x;
  const IMAGE_src1_PIXEL_TYPE input1 = READ_src1_IMAGE(src1, sampler, pos).x;

  const IMAGE_dst_PIXEL_TYPE value = CONVERT_dst_PIXEL_TYPE(max(input, input1));

  WRITE_dst_IMAGE(dst, pos, value);
}
