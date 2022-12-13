import pandas as pd
import seaborn as sns
import sweetviz as sv

if __name__ == "__main__":
    df = pd.read_csv('../../data/raw/heart_cleveland_upload.csv')
    svm = sns.heatmap(df.corr())
    figure = svm.get_figure()
    figure.savefig('../../reports/figures/svm_conf.png')

    report = sv.analyze([df, 'Heart'])
    report.show_html('../../reports/heart_cleveland_EDA.html',
                     open_browser=False)
