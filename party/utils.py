from subprocess import Popen, PIPE


def run(args):
    process = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        raise Exception(stderr.decode("utf-8"))
    return stdout.decode("utf-8")


def partify(src_path, data):
    args = get_args(data)
    return run(['bash', 'gifit.sh', src_path, "".join(args)] + args)


def get_args(data):
    args = []
    if data.get('resize'):
        args += ['-r', data['resize']]
    if data.get('n_frames'):
        args += ['-n', data['n_frames']]
    if data.get('delay'):
        args += ['-d', data['delay']]
    if data.get('fuzz'):
        args += ['-f', data['fuzz']]
    method = data.get('method')
    if method == 'hue_rotate':
        args += ['-h']
        # TODO doesn't work with replace color!
        # need to do negate before replace color
        if data.get('negate'):
            args += ['-N', data['negate']]
    if method == 'replace_color':
        args += ['-R', data.get('replace_color')]
    args = [str(arg) for arg in args]
    return args


def get_n_frames(path):
    return len(run(['identify',self.src.path]).strip().split('\n'))


def get_colors(path):
    # get raw histogram
    histogram = run(['convert',self.src.path,"+dither",'-format','%c','histogram:info:'])

    # trim whitespace, remove empty lines
    histogram = [l.strip() for l in histogram.split('\n') if l]

    # sort by most occurrence
    histogram = sorted(
        histogram,
        key=lambda s: int(s.split(':')[0]),
        reverse=True
    )

    # ignore zero alpha
    histogram = [l for l in histogram if not ',  0)' in l]

    colors = []
    matched = []
    for line in histogram:
        if len(self.colors) > 10:
            break
        count = int(line.split(':')[0])
        color = line.split(' ')[-1]
        if color in matched:
            continue
        matched.append(color)
        colors.append({
            'color': color,
            'count': count,
        })

    return colors
