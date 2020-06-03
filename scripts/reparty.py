import django, os;os.environ['DJANGO_SETTINGS_MODULE'] = 'server.settings';django.setup()

from party.models import PartyImage

for pi in PartyImage.objects.all():
  if pi.sourceimage_id in [4, 69]:
    continue
  if pi.sourceimage.partyimage_set.count() > 0:
    # print(pi.id)
    # print(pi.sourceimage.get_variants_for_user())
    # exit()
    if not os.path.exists(pi.src.path):
      print('partying', pi)
      pi.party()