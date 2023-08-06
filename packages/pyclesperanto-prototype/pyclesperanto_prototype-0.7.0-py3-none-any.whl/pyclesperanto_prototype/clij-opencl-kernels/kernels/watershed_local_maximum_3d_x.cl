__kernel void watershed_local_maximum_3d
(
  IMAGE_src_labelmap_TYPE src_labelmap,
  IMAGE_src_distancemap_TYPE src_distancemap,
  IMAGE_dst_labelmap_TYPE dst_labelmap,
  IMAGE_dst_distancemap_TYPE dst_distancemap,
  IMAGE_flag_dst_TYPE flag_dst
)
{
  const sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;

  const int x = get_global_id(0);
  const int y = get_global_id(1);
  const int z = get_global_id(2);

  const int4 pos = (int4){x,y, z, 0};

  float currentlabel = READ_src_labelmap_IMAGE(src_labelmap, sampler, pos).x;
  float currentdistance = READ_src_distancemap_IMAGE(src_distancemap, sampler, pos).x;

  float bestlabel = currentlabel;
  float bestdistance = currentdistance;

  if (currentdistance > 0) {
      for (int ax = -1; ax <= 1; ax++) {
        for (int ay = -1; ay <= 1; ay++) {
          for (int az = -1; az <= 1; az++) {
            float distance = READ_src_distancemap_IMAGE(src_distancemap, sampler, (pos + (int4){ax, ay, az, 0})).x;
            if (distance > 0) {
              if (distance > bestdistance) {
                float label = READ_src_labelmap_IMAGE(src_labelmap, sampler, (pos + (int4){ax, ay, az, 0})).x;
                bestdistance = distance;
                bestlabel = label;
              }
            }
          }
        }
      }

    if (fabs(((float)bestlabel - currentlabel)) > 0) {
      WRITE_flag_dst_IMAGE(flag_dst,(int4)(0,0,0,0),1);
    }
  }
  WRITE_dst_labelmap_IMAGE (dst_labelmap, pos, CONVERT_dst_labelmap_PIXEL_TYPE(bestlabel));
  WRITE_dst_distancemap_IMAGE (dst_distancemap, pos, CONVERT_dst_distancemap_PIXEL_TYPE(bestdistance));
}
