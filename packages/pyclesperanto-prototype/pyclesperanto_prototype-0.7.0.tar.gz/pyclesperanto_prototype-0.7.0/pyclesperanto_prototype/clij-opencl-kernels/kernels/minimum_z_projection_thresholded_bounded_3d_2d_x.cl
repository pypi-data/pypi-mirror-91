
__kernel void minimum_z_projection_thresholded_bounded_3d_2d(
    IMAGE_dst_min_TYPE dst_min,
    IMAGE_src_TYPE src,
    float threshold_intensity,
    int min_z,
    int max_z
) {
  const sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;

  const int x = get_global_id(0);
  const int y = get_global_id(1);
  float min = 0;

  int start = 0;
  if (min_z > start) {
    start = min_z;
  }

  int end = GET_IMAGE_DEPTH(src) - 1;
  if (max_z < end) {
    end = max_z;
  }

  bool initialized = 0;
  for(int z = start; z <= end; z++)
  {
    float value = READ_src_IMAGE(src,sampler,(int4)(x,y,z,0)).x;
    if ((threshold_intensity < value) && (value < min || initialized == 0)) {
      min = value;
      initialized = 1;
    }
  }
  WRITE_dst_min_IMAGE(dst_min,(int2)(x,y), CONVERT_dst_min_PIXEL_TYPE(min));
}