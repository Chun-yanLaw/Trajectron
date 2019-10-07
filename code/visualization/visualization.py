from utils import prediction_output_to_trajectories
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe


def plot_trajectories(ax,
                      prediction_dict,
                      histories_dict,
                      futures_dict,
                      line_alpha=0.7,
                      line_width=0.2,
                      edge_width=2,
                      circle_edge_width=0.5,
                      node_circle_size=0.3):

    for node_name in histories_dict:
        history = histories_dict[node_name]
        future = futures_dict[node_name]
        predictions = prediction_dict[node_name]

        ax.plot(history[:, 0], history[:, 1], 'k--')

        for sample_num in range(prediction_dict[node_name].shape[0]):
            ax.plot(predictions[sample_num, :, 0], predictions[sample_num, :, 1],
                    color='blue',
                    linewidth=line_width, alpha=line_alpha)

            ax.plot(future[:, 0],
                    future[:, 1],
                    'w--',
                    path_effects=[pe.Stroke(linewidth=edge_width, foreground='k'), pe.Normal()])

            # Current Node Position
            circle = plt.Circle((history[-1, 0],
                                 history[-1, 1]),
                                node_circle_size,
                                facecolor='g',
                                edgecolor='k',
                                lw=circle_edge_width,
                                zorder=3)
            ax.add_artist(circle)

    # Robot Node # TODO Robot Node
    # if robot_node is not None:
    #     prefix_earliest_idx = max(0, t_predict - predict_horizon)
    #     robot_prefix = inputs[robot_node][0, prefix_earliest_idx : t_predict + 1, 0:2].cpu().numpy()
    #     robot_future = inputs[robot_node][0, t_predict + 1 : min(t_predict + predict_horizon + 1, traj_length), 0:2].cpu().numpy()
    #
    #     prefix_all_zeros = not np.any(robot_prefix)
    #     future_all_zeros = not np.any(robot_future)
    #     if not (prefix_all_zeros and future_all_zeros):
    #         ax.plot(robot_prefix[:, 0], robot_prefix[:, 1], 'k--')
    #         ax.plot(robot_future[:, 0], robot_future[:, 1], 'w--',
    #                 path_effects=[pe.Stroke(linewidth=edge_width, foreground='k'), pe.Normal()])
    #
    #         circle = plt.Circle((robot_prefix[-1, 0],
    #                              robot_prefix[-1, 1]),
    #                             node_circle_size,
    #                             facecolor='g',
    #                             edgecolor='k',
    #                             lw=circle_edge_width,
    #                             zorder=3)
    #         ax.add_artist(circle)
    #
    #         # Radius of influence
    #         if robot_circle:
    #             circle = plt.Circle((robot_prefix[-1, 0], robot_prefix[-1, 1]), test_stg.hyperparams['edge_radius'],
    #                                 fill=False, color='r', linestyle='--', zorder=3)
    #             ax.plot([], [], 'r--', label='Edge Radius')
    #             ax.add_artist(circle)


def visualize_prediction(ax,
                         prediction_output_dict,
                         dt,
                         max_hl,
                         ph,
                         robot_node=None,
                         **kwargs):

    prediction_dict, histories_dict, futures_dict = prediction_output_to_trajectories(prediction_output_dict,
                                                                                      dt,
                                                                                      max_hl,
                                                                                      ph)

    assert(len(prediction_dict.keys()) <= 1)
    if len(prediction_dict.keys()) == 0:
        return
    ts_key = list(prediction_dict.keys())[0]
    prediction_dict = prediction_dict[ts_key]
    histories_dict = histories_dict[ts_key]
    futures_dict = futures_dict[ts_key]

    plot_trajectories(ax, prediction_dict, histories_dict, futures_dict, *kwargs)