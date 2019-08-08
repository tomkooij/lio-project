
def find_peaks(trace, threshold=20):
    """Find peaks in trace

    returns list of tuples: (t, pulseheight, pulseintegral) for each peak
    t = 0 for first peak
    """

    peaks = []
    peak_idxs = []
    in_peak = False
    t_end = 0

    trace.append(0)  # add 0 to make sure last peak is detected

    for t, value in enumerate(trace):
        if in_peak:
            if value > threshold:
                continue
            else:
                # end of peak
                in_peak = False
                t_end = t
                peak_idxs.append((t_start, t_end))
        else:
            # not in peak
            if value > threshold:
                in_peak = True
                t_start = t

    if len(peak_idxs):
        t0 = peak_idxs[0][0]
        for t_start, t_end in peak_idxs:
            peak = trace[t_start:t_end]
            peaks.append(((t_start - t0) * 2.5, max(peak), sum(peak)))

    return peaks


if __name__ == '__main__':
    trace = [9, 0, -12, 30, 30, 30, 45, 0, 0, 20, 20, 20, 21, 22, 0, 50]
    print(find_peaks(trace))
