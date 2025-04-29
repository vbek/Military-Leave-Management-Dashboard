def show_analytics(self, frame_class, frame_buttons):
    import matplotlib
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
    from tkinter import Toplevel, Button, Frame
    from datetime import datetime
    matplotlib.use('TkAgg')

    popup = Toplevel(self)
    popup.title("Analytics Graph")
    popup.geometry("1000x600")

    analytics_figures = []
    current_index = [0]
    canvas = [None]

    from CreateConnection import CreateConnection
    obj_cc = CreateConnection(database_name='bibekdb')
    conn = obj_cc.create_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES LIKE 'leave_record_%'")
    leave_tables = cursor.fetchall()

    count_over_90 = 0
    count_under_90 = 0
    currently_at_home = 0
    seen_compnos = set()

    rank_leave_counts = {}
    loc_counts = {}

    for (table_name,) in leave_tables:
        cursor.execute(f"SELECT CompNo, LeaveDate, ReturnDate FROM {table_name}")
        rows = cursor.fetchall()

        for compno, leave_date, return_date in rows:
            if compno in seen_compnos:
                continue
            seen_compnos.add(compno)

            try:
                cursor.execute(f"SELECT rnk, Loc FROM kalidal_bn WHERE CompNo = %s", (compno,))
                rank_loc_row = cursor.fetchone()
                if rank_loc_row:
                    rnk, loc = rank_loc_row
                    if rnk not in rank_leave_counts:
                        rank_leave_counts[rnk] = 0
                    if loc not in loc_counts:
                        loc_counts[loc] = 0

                    if not return_date or return_date == '0000-00-00':
                        currently_at_home += 1
                        loc_counts[loc] += 1
                    else:
                        return_dt = datetime.strptime(str(return_date), "%Y-%m-%d").date()
                        today = datetime.now().date()
                        if return_dt > today:
                            currently_at_home += 1
                            loc_counts[loc] += 1
                        else:
                            days_since = (today - return_dt).days
                            if days_since > 90:
                                count_over_90 += 1
                            else:
                                count_under_90 += 1
                            rank_leave_counts[rnk] += 1
                            loc_counts[loc] += 1
            except Exception as e:
                print(f"Error parsing date: {return_date}, error: {e}")

    cursor.close()
    conn.close()

    # === CHART DEFINITIONS ===
    def create_bar_chart():
        fig, ax = plt.subplots(figsize=(6, 4))
        labels = ['>90 Days', '≤90 Days', 'At Home']
        values = [count_over_90, count_under_90, currently_at_home]
        ax.bar(labels, values, color=['red', 'orange', 'green'])
        ax.set_ylabel("Number of Members")
        ax.set_title("Home Leave Status (Bar Chart)")
        return fig

    def create_rank_histogram():
        fig, ax = plt.subplots(figsize=(10, 6))
        ranks = list(rank_leave_counts.keys())
        leave_counts = list(rank_leave_counts.values())
        bars = ax.bar(ranks, leave_counts, color='purple')
        ax.set_ylabel("Number of People on Leave", fontsize=10)
        ax.set_xlabel("Rank", fontsize=8)
        ax.set_title("Distribution by Rank", fontsize=12)
        ax.set_xticks(ranks)
        ax.set_xticklabels(ranks, rotation=90, fontsize=6)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, str(height),
                    ha='center', va='bottom', fontsize=8)
        plt.tight_layout()
        return fig

    def create_loc_chart():
        fig, ax = plt.subplots(figsize=(12, 6))  # Wider to accommodate more labels
        locs = list(loc_counts.keys())
        counts = list(loc_counts.values())

        locs_counts_sorted = sorted(zip(locs, counts), key=lambda x: x[1], reverse=True)
        locs, counts = zip(*locs_counts_sorted)

        bars = ax.bar(locs, counts, color='teal')
        ax.set_ylabel("Counts", fontsize=10)
        ax.set_xlabel("Location", fontsize=9)
        ax.set_title("Distribution by Location", fontsize=12)

        ax.set_xticks(range(len(locs)))
        ax.set_xticklabels(locs, rotation=45, ha='right', fontsize=8)

        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, str(height),
                    ha='center', va='bottom', fontsize=8)

        plt.tight_layout()
        return fig

    def create_bloodgp_chart():
        # Open connection inside the chart function
        obj_cc = CreateConnection(database_name='bibekdb')
        conn = obj_cc.create_connection()
        cursor = conn.cursor()

        bloodgp_counts = {}
        cursor.execute("SELECT bloodgp, COUNT(*) FROM kalidal_bn GROUP BY bloodgp")
        for bloodgp, count in cursor.fetchall():
            bloodgp_counts[bloodgp] = count

        cursor.close()
        conn.close()

        fig, ax = plt.subplots(figsize=(8, 5))
        bloodgps = list(bloodgp_counts.keys())
        counts = list(bloodgp_counts.values())

        # Assign distinct colors manually or use a colormap
        predefined_colors = {
            'O +ve': 'red',
            'A +ve': 'blue',
            'B +ve': 'green',
            'AB +ve': 'orange',
            'O -ve': 'purple',
            'A -ve': 'cyan',
            'B -ve': 'yellow',
            'AB -ve': 'brown'
        }

        colors = [predefined_colors.get(bg, 'gray') for bg in bloodgps]

        bars = ax.bar(bloodgps, counts, color=colors)
        ax.set_ylabel("Counts", fontsize=10)
        ax.set_xlabel("Blood Group", fontsize=9)
        ax.set_title("Distribution by Blood Group", fontsize=12)

        ax.set_xticks(range(len(bloodgps)))
        ax.set_xticklabels(bloodgps, fontsize=9)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, str(height),
                    ha='center', va='bottom', fontsize=8)

        plt.tight_layout()
        return fig

    # === APPEND CHARTS ===
    analytics_figures.append(create_bar_chart())
    analytics_figures.append(create_rank_histogram())
    analytics_figures.append(create_loc_chart())
    analytics_figures.append(create_bloodgp_chart())  # 👈 blood group chart with DB inside

    # === GUI Functions ===
    def render_chart(index):
        if canvas[0]:
            canvas[0].get_tk_widget().destroy()
        fig = analytics_figures[index]
        new_canvas = FigureCanvasTkAgg(fig, master=popup)
        new_canvas.draw()
        new_canvas.get_tk_widget().pack(expand=True)
        canvas[0] = new_canvas

    def show_next():
        current_index[0] = (current_index[0] + 1) % len(analytics_figures)
        render_chart(current_index[0])

    def show_prev():
        current_index[0] = (current_index[0] - 1) % len(analytics_figures)
        render_chart(current_index[0])

    def on_close():
        try:
            if canvas[0]:
                canvas[0].get_tk_widget().destroy()
            popup.destroy()
        except Exception as e:
            print(f"Popup close error: {e}")

    popup.protocol("WM_DELETE_WINDOW", on_close)

    nav_frame = Frame(popup)
    nav_frame.pack(side='bottom', pady=10)

    prev_button = Button(nav_frame, text="◀ Previous", command=show_prev)
    prev_button.pack(side='left', padx=10)

    next_button = Button(nav_frame, text="Next ▶", command=show_next)
    next_button.pack(side='right', padx=10)

    render_chart(current_index[0])
