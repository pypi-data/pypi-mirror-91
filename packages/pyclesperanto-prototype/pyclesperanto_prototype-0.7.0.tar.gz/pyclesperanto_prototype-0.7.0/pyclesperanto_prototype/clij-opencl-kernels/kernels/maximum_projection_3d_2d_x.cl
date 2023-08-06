
__kernel void maximum_projection_3d_2d(
    IMAGE_dst_TYPE dst,
    IMAGE_src_TYPE src
) {
  const sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;

  const int x = get_global_id(0);
  const int y = get_global_id(1);
  float max = 0;
  for(int z = 0; z < GET_IMAGE_DEPTH(src); z++)
  {
    float value = READ_src_IMAGE(src,sampler,(int4)(x,y,z,0)).x;
    if (value > max || z == 0) {
      max = value;
    }
  }
  WRITE_dst_IMAGE(dst,(int2)(x,y), CONVERT_dst_PIXEL_TYPE(max));
}
