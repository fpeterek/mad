import click
import tkinter
import tkinter.filedialog

import austin


@click.command()
@click.option('--input-file', default='in/austin.csv', help='Input dataset')
@click.option('--clusters', default=7, help='Number of clusters (max=7)')
@click.option('--attempts', default=5, help='Max clustering attempts')
@click.option('--processes', default=4, help='Number of processes')
@click.option('--sil-idx', default=False, help='Calculate silhouette index')
@click.option('--k-means', default=True, help='Apply k-means')
def run_ui(input_file: str, clusters: int, attempts: int, processes: int, sil_idx: bool, k_means: bool):
    tk = tkinter.Tk()
    infile_label = tkinter.Label(tk, text=f'Input file: {input_file}')

    def select_file():
        return tkinter.filedialog.askopenfilename(initialfile=input_file)

    def set_file():
        nonlocal input_file
        nonlocal infile_label
        input_file = select_file()
        infile_label.config(text=f'Input file: {input_file}')

    infile_button = tkinter.Button(tk, text='Select file', command=set_file)
    cluster_var = tkinter.IntVar(value=clusters)
    cluster_scale = tkinter.Scale(tk, variable=cluster_var, orient=tkinter.HORIZONTAL)
    cluster_label = tkinter.Label(tk, text='Clusters')
    attempts_var = tkinter.IntVar(value=attempts)
    attempts_scale = tkinter.Scale(tk, variable=attempts_var, orient=tkinter.HORIZONTAL)
    attempts_label = tkinter.Label(tk, text='Attempts')
    processes_var = tkinter.IntVar(value=processes)
    processes_scale = tkinter.Scale(tk, variable=processes_var, orient=tkinter.HORIZONTAL)
    processes_label = tkinter.Label(tk, text='Processes')
    sil_idx_var = tkinter.BooleanVar(value=sil_idx)
    sil_idx_button = tkinter.Checkbutton(tk, variable=sil_idx_var, text='Silhouette index')
    kmeans_var = tkinter.BooleanVar(value=k_means)
    kmeans_button = tkinter.Checkbutton(tk, variable=kmeans_var, text='K-means')

    def button_run():
        austin.run(input_file=input_file, clusters=cluster_var.get(), attempts=attempts_var.get(),
                   processes=processes_var.get(), sil_idx=sil_idx_var.get(), apply_kmeans=kmeans_var.get())
        tk.destroy()

    run_button = tkinter.Button(tk, text='Run', command=button_run)

    infile_label.pack(anchor='w')
    infile_button.pack(anchor='w')
    cluster_label.pack(anchor='w')
    cluster_scale.pack(anchor='w')
    attempts_label.pack(anchor='w')
    attempts_scale.pack(anchor='w')
    processes_label.pack(anchor='w')
    processes_scale.pack(anchor='w')
    sil_idx_button.pack(anchor='w')
    kmeans_button.pack(anchor='w')
    run_button.pack()
    tk.mainloop()

