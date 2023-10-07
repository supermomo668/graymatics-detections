data_home=data/agrosuper
mkdir -p $data_home


gdown --fuzzy "https://drive.google.com/file/d/1SESZ9CTQEtme9hocTWlFrWfwDDPIChhV/view?usp=drive_link" -O $data_home/
gdown --fuzzy "https://drive.google.com/file/d/11XSf0N2_KNxTEzke-ypJsQZ_kx4iJsCV/view?usp=drive_link" -O $data_home/
gdown --fuzzy "https://drive.google.com/file/d/1ASb-71SaiuJbLbdVJnqZyM3oen5YJoap/view?usp=drive_link" -O $data_home/

# unzip data/annotations_agrosuper-20231003T064856Z-001.zip -d $data_home
# unzip data/frames_agrosuper-20231003T064847Z-001.zip -d $data_home
# unzip data/annotations_Isabella.zip -d $data_home
unzip '*.zip'


frames_home=$data_home/frames
mkdir -p $frames_home
annot_home=$data_home/annotations
mkdir -p $annot_home

mv -f $data_home/annotations_agrosuper/* $annot_home && rm -r $data_home/annotations_agrosuper
mv -f $data_home/frames_agrosuper/* $frames_home && rm -r $data_home/frames_agrosuper

mv -f $data_home/new_annotations/annotations_isabella/*.jpg $frames_home
mv -f $data_home/new_annotations/annotations_isabella/*.xml $annot_home
rm -r $data_home/new_annotations