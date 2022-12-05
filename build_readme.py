notebooks = [
    ("Advent of Code (2022)", "/pytudes/blob/master/ipynb/Advent%20of%20Code%202022.ipynb"),
    ("Advent of Code (2021)", "/pytudes/blob/master/ipynb/Advent%20of%20Code%202021.ipynb"),
    ("Advent of Code (2020)", "/pytudes/blob/master/ipynb/Advent%20of%20Code%202020.ipynb"),
    ("Advent of Code (2019)", "/pytudes/blob/master/ipynb/Advent%20of%20Code%202019.ipynb"),
    ("Advent of Code (2018)", "/pytudes/blob/master/ipynb/Advent%20of%20Code%202018.ipynb"),
    ("Advent of Code (2017)", "/pytudes/blob/master/ipynb/Advent%20of%20Code%202017.ipynb"),
    ("Advent of Code (2016)", "/pytudes/blob/master/ipynb/Advent%20of%20Code%202016.ipynb"),
]

def build_links(path: str):
    return [
        f"[n](https://nbviewer.org/github/willcodefortea{path})",
        f"[s](https://studiolab.sagemaker.aws/import/github/willcodefortea{path})",
    ]

def _gh_link(title: str, path: str):
    return f"[{title}](https://github.com/willcodefortea/{path})"

def build_table():
    rows = "\n".join([
        f"| {' '.join(build_links(path))} | {_gh_link(title, path)} |"
        for (title, path) in notebooks
    ])
    return f"""| Run | Title |
| --- | --- |
{rows}
"""

def build_readme():
    body = f"""# pytudes

Small programs to practice Kata and Advent of Code!

To get going, install a copy of [jypter notebook](http://jupyter.org/) and run `jupyter notebook`, navigate the notebook you're interested in and you're done.

## Notebooks

For each notebook you can:

* Click on n to view the notebook on NBViewer
* Click on s to view the notebook on sagemaker
* Click on the title to view the notebook on github

{build_table()}
"""
    return body

def main():
    with open("README.md", "w") as fout:
        readme = build_readme()
        fout.write(readme)

if __name__ == "__main__":
    main()