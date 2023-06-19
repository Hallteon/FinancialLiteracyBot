# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.patches import Circle, RegularPolygon
# from matplotlib.path import Path
# from matplotlib.projections.polar import PolarAxes
# from matplotlib.projections import register_projection
# from matplotlib.spines import Spine
# from matplotlib.transforms import Affine2D
#
#
# def radar_factory(num_vars, frame='circle'):
#     theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
#
#     class RadarTransform(PolarAxes.PolarTransform):
#
#         def transform_path_non_affine(self, path):
#             if path._interpolation_steps > 1:
#                 path = path.interpolated(num_vars)
#             return Path(self.transform(path.vertices), path.codes)
#
#     class RadarAxes(PolarAxes):
#
#         name = 'radar'
#         PolarTransform = RadarTransform
#
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             self.set_theta_zero_location('N')
#
#         def fill(self, *args, closed=True, **kwargs):
#             return super().fill(closed=closed, *args, **kwargs)
#
#         def plot(self, *args, **kwargs):
#             lines = super().plot(*args, **kwargs)
#             for line in lines:
#                 self._close_line(line)
#
#         def _close_line(self, line):
#             x, y = line.get_data()
#             if x[0] != x[-1]:
#                 x = np.append(x, x[0])
#                 y = np.append(y, y[0])
#                 line.set_data(x, y)
#
#         def set_varlabels(self, labels):
#             self.set_thetagrids(np.degrees(theta), labels)
#
#         def _gen_axes_patch(self):
#             if frame == 'circle':
#                 return Circle((0.5, 0.5), 0.5)
#             elif frame == 'polygon':
#                 return RegularPolygon((0.5, 0.5), num_vars,
#                                       radius=.5, edgecolor="k")
#             else:
#                 raise ValueError("Unknown value for 'frame': %s" % frame)
#
#         def _gen_axes_spines(self):
#             if frame == 'circle':
#                 return super()._gen_axes_spines()
#             elif frame == 'polygon':
#                 spine = Spine(axes=self,
#                               spine_type='circle',
#                               path=Path.unit_regular_polygon(num_vars))
#                 spine.set_transform(Affine2D().scale(.6).translate(.6, .6)
#                                     + self.transAxes)
#                 return {'polar': spine}
#             else:
#                 raise ValueError("Unknown value for 'frame': %s" % frame)
#
#     register_projection(RadarAxes)
#     return theta
#
#
# def generate_chart_data(data):
#     chart_data = [
#         [section['section_name'] for section in data.values()],
#         ('Колесо финансового баланса', [[section['total_points'] for section in data.values()]])]
#
#     return chart_data
#
#
# def get_radar_chart(data):
#     N = len(data[0])
#     theta = radar_factory(N, frame='polygon')
#     spoke_labels = data.pop(0)
#
#     fig, axs = plt.subplots(figsize=(N, N), nrows=1, ncols=1,
#                             subplot_kw=dict(projection='radar'))
#
#     colors = ['b']
#     for (title, case_data) in data:
#         axs.set_rgrids([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
#         axs.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
#                      horizontalalignment='center', verticalalignment='center')
#         for d, color in zip(case_data, colors):
#             axs.plot(theta, d, color=color)
#             axs.fill(theta, d, facecolor=color, alpha=0.25, label='_nolegend_')
#
#         axs.set_varlabels(spoke_labels)
#
#     return plt

import numpy as np
import matplotlib.pyplot as plt


def get_radar_chart(data):
    results = [{section['section_name']: section['total_points'] for section in data.values()}]
    data_length = len(results[0])
    angles = np.linspace(0, 2 * np.pi, data_length, endpoint=False)
    labels = [key for key in results[0].keys()]
    score = [[v for v in result.values()] for result in results]

    score_a = np.concatenate((score[0], [score[0][0]]))

    angles = np.concatenate((angles, [angles[0]]))
    labels = np.concatenate((labels, [labels[0]]))
    fig = plt.figure(figsize=(8, 6), dpi=100)
    ax = plt.subplot(111, polar=True)

    ax.plot(angles, score_a, color='g')
    ax.set_thetagrids(angles * 180 / np.pi, labels)
    ax.set_theta_zero_location('N')
    ax.set_rlim(0, 10)
    ax.set_rlabel_position(270)
    ax.set_title('Колесо финансового баланса')

    return plt




