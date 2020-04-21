import _scripts
import os
import re

from django.conf import settings

from party import utils
from server.models import PartyImage, SourceImage

PARTY_DIR = os.path.join(settings.MEDIA_ROOT, '.party')
FS_DIRS = []
DB_DIRS = []
DB_MAP = {}

PartyImage.objects.all().delete()

# tina = SourceImage.objects.get(src__icontains='tina.gif')
# for pi in tina.partyimage_set.all():
#   print(pi.replace_color)
#   print(pi.party_dir)
#   print()
# exit()

for filename in os.listdir(PARTY_DIR):
  if filename.endswith('.log'):
    continue
  try:
    si = SourceImage.objects.get(src__endswith='/'+filename)
  except SourceImage.DoesNotExist:
    print(f"SourceImage for {filename} does not exist")
    continue
  variants = os.listdir(os.path.join(PARTY_DIR, filename))

  # at somepoint I accidentally added -h to arguments even though it was unnecessary
  for variant in [v for v in variants if '-h' in v]:
    new_name = variant.replace("-h", '')
    if new_name in variants:
      raise NotImplementedError('Redundant folder exists')
    os.rename(
      os.path.join(PARTY_DIR, filename, variant),
      os.path.join(PARTY_DIR, filename, new_name)
    )
    print(f"renamed {variant} to {new_name}")
    variant = new_name

  # reload in case previous step changed anything
  variants = os.listdir(os.path.join(PARTY_DIR, filename))
  for variant in variants:
    FS_DIRS.append(filename+'/'+variant)
    partyimage = PartyImage.get_from_dict(si.id, utils.flagstr_to_dict(variant))
    full_party_dir = os.path.join(settings.MEDIA_ROOT, '.party', partyimage.party_dir)
    DB_DIRS.append(partyimage.party_dir)
    if '-r' in variant and not os.path.exists(full_party_dir):
      print('dir missing', variant, full_party_dir)

# for fs_dir in FS_DIRS:
#   db_dir = fs_dir.replace('-h', '')
#   db_dir = re.sub(r'-r\d+', '', db_dir)
#   if not db_dir in DB_DIRS:
#     print(db_dir)

# print('---')
# for db_dir in DB_DIRS:
#   if 'tina' in db_dir:
#     print(db_dir)

