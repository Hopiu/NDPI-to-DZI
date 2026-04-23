rclone copy \
  /home/bw/Documents/Zahnmedizin \
  "histology:html/Präparate/Zahnmedizin" \
  --transfers 8 \
  --checkers 16 \
  --progress \
  --log-file=rclone_upload.log

# rclone copy \
#   /home/bw/Workspace/NDPI2DZI/output/Zahnschliff.dzi \
#   "histology:files/html/Präparate/Zahnmedizin/" \
#   --progress