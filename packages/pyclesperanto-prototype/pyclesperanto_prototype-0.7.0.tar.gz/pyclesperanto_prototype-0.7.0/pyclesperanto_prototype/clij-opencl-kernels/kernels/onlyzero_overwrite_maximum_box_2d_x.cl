__constant sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;

__kernel void onlyzero_overwrite_maximum_box_2d
(
  IMAGE_dst_TYPE dst,
  IMAGE_flag_dst_TYPE flag_dst,
  IMAGE_src_TYPE src
)
{
  const int x = get_global_id(0);
  const int y = get_global_id(1);

  const int2 pos = (int2){x,y};

  float foundMaximum = READ_src_IMAGE(src, sampler, pos).x;
  if (foundMaximum == 0) {
      float originalValue = foundMaximum;
      float value = READ_src_IMAGE(src, sampler, (pos + (int2){1, 0})).x;
      if ( value > foundMaximum && value > 0) {
        foundMaximum = value;
      }
      value = READ_src_IMAGE(src, sampler, (pos + (int2){-1, 0})).x;
      if ( value > foundMaximum && value > 0) {
        foundMaximum = value;
      }
      value = READ_src_IMAGE(src, sampler, (pos + (int2){0, 1})).x;
      if ( value > foundMaximum && value > 0) {
        foundMaximum = value;
      }
      value = READ_src_IMAGE(src, sampler, (pos + (int2){0, -1})).x;
      if ( value > foundMaximum && value > 0) {
        foundMaximum = value;
      }

        value = READ_src_IMAGE(src, sampler, (pos + (int2){1, 1})).x;
        if ( value > foundMaximum && value > 0) {
          foundMaximum = value;
        }
        value = READ_src_IMAGE(src, sampler, (pos + (int2){-1, 1})).x;
        if ( value > foundMaximum && value > 0) {
          foundMaximum = value;
        }
        value = READ_src_IMAGE(src, sampler, (pos + (int2){-1, -1})).x;
        if ( value > foundMaximum && value > 0) {
          foundMaximum = value;
        }
        value = READ_src_IMAGE(src, sampler, (pos + (int2){1, -1})).x;
        if ( value > foundMaximum && value > 0) {
          foundMaximum = value;
        }

      if (foundMaximum != originalValue) {
        WRITE_flag_dst_IMAGE(flag_dst,(int4)(0,0,0,0),1);
      }
  }
  WRITE_dst_IMAGE(dst, pos, CONVERT_dst_PIXEL_TYPE(foundMaximum));
}