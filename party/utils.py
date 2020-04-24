from collections import defaultdict
from subprocess import Popen, PIPE

# DEFINITIONS
# flag - the one-letter bash code for a flag
# field - the name of the field on PartyImage model
# flagstr - the "flag string" used to save PartyImages under like -n12-d6-f3-h-Ngreen
# flagkwargs - PartyImage flags as a dict

N_FRAMES = 7
DELAY = 12


def clean_flagkwargs(flagkwargs):
    # some arguments don't work together
    if flagkwargs['method'] == 'replace_color':
        if not flagkwargs.get('replace_color'):
            raise ValueError("Cannot have replace color without specifying a color")
        flagkwargs.pop('negate_channel', None)
    elif flagkwargs['method'] == 'hue_rotate':
        flagkwargs.pop('replace_color', None)
        flagkwargs.pop('fuzz', None)
    # for now just hard code this since its fixed on front end
    flagkwargs['n_frames'] = flagkwargs.get('n_frames') or N_FRAMES

    # everything except method can be None
    for field in PARTY_FIELDS:
        if field != 'method':
            flagkwargs[field] = flagkwargs.get(field, None)
    return flagkwargs


PARTY_FIELDS = ['n_frames', 'fuzz', 'method', 'negate_channel', 'replace_color']
FLAG_TO_FIELD = {
    'R': 'replace_color',
    'N': 'negate_channel',
}

for field in PARTY_FIELDS:
    if field in FLAG_TO_FIELD.values():
        continue
    FLAG_TO_FIELD[field[0]] = field


def flagstr_to_dict(flagstr):
    out = {}
    for flag_pair in flagstr.split('-'):
        if not flag_pair or flag_pair[0] == 'r':
            continue
        flag = flag_pair[0]
        field = FLAG_TO_FIELD[flag]
        value = flag_pair[1:]
        out[field] = value
    if out.get('replace_color'):
        if out.get('method', 'replace_color') != 'replace_color':
            raise NotImplementedError()
        out['method'] = 'replace_color'
    return out


def run(args):
    process = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        raise Exception(stderr.decode("utf-8"))
    return stdout.decode("utf-8")


def partify(src_path, output_root, data, output_filename=None):
    args = get_args(data)
    dest_dir = output_root + "/" + "".join(args)
    if output_filename:
        args += ['-o', output_filename]
    return run(['bash', 'gifit.sh', src_path, dest_dir] + args)


def get_args(data):
    args = []
    if data.get('n_frames'):
        args += ['-n', data['n_frames']]
    if data.get('delay'):
        args += ['-d', data['delay']]
    if data.get('fuzz'):
        args += ['-f', data['fuzz']]
    method = data.get('method')
    if method == 'hue_rotate':
        # TODO doesn't work with replace color!
        # need to do negate before replace color
        if data.get('negate_channel'):
            args += ['-N', data['negate_channel']]
        if data.get('replace_color'):
            raise NotImplementedError(f"bad data {data}")
    if method == 'replace_color':
        args += ['-R', data.get('replace_color')]
    args = [str(arg) for arg in args]
    return args


def get_n_frames(path):
    return len(run(['identify', path]).strip().split('\n'))


def get_colors(path):
    # get raw histogram
    histogram = run(['convert', path, "+dither", '-format', '%c', 'histogram:info:'])

    # trim whitespace, remove empty lines
    histogram = [l.strip() for l in histogram.split('\n') if l]

    # sort by most occurrence
    histogram = sorted(histogram, key=lambda s: int(s.split(':')[0]), reverse=True)

    # ignore zero alpha
    histogram = [l for l in histogram if not ',  0)' in l]

    counts = defaultdict(int)
    matched = []
    for line in histogram:
        count = int(line.split(':')[0])
        color = line.split(' ')[-2][:7]
        counts[color] += count

    items = sorted(counts.items(), key=lambda i: i[1], reverse=True)

    return items[:10]
