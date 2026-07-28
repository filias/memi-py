"""memi pyrenees — practise your memory of the Pyrenees."""

from memi_engine import MemiConfig, create_app

import memi_py.providers  # noqa: F401  (import registers the providers)

config = MemiConfig(
    analytics_html=(
        '<script data-goatcounter="https://memi-py.goatcounter.com/count"'
        ' async src="//gc.zgo.at/count.js"></script>'
    ),
    title="memi pyrenees",
    subtitle="name the peaks, wildlife and lakes",
    wikipedia_lang="en",
    favicon_color="#2f6b3d",
    sponsor_url="https://github.com/sponsors/filias",
    sponsor_text="sponsor",
    related_sites=[
        {"name": "memi", "url": "https://memi.click"},
        {"name": "memi portugal", "url": "https://pt.memi.click"},
        {"name": "memi lisboa", "url": "https://lx.memi.click"},
        {"name": "memi slovensko", "url": "https://sk.memi.click"},
        {"name": "memi US", "url": "https://us.memi.click"},
    ],
    about_html="""
        <p>memi pyrenees is a memory practice game about the Pyrenees &mdash;
        the mountain range straddling France, Spain and Andorra. Peaks,
        wildlife, lakes, valleys and passes: there's always something to
        remember.</p>

        <h2>How to play</h2>
        <p>Pick a category, look at the image, and try to name it before
        revealing the answer. No accounts, no scores, no time limits.</p>
        <ul>
            <li><strong>clues:</strong> toggle progressive letter hints.</li>
            <li><strong>know more:</strong> appears on reveal and opens the
            Wikipedia article for the item.</li>
            <li><strong>report:</strong> flag a card if the image doesn't match
            the answer.</li>
        </ul>

        <h2>Why it works</h2>
        <p>This is a simple form of <em>active recall</em> &mdash; pulling a
        name out of memory instead of re-reading it. Retrieval practice builds
        more durable memory than re-exposure alone, and because each prompt is a
        picture it also leans on the <em>picture superiority effect</em>. Short,
        frequent sessions beat long ones.</p>
    """,
)

app = create_app(config)

if __name__ == "__main__":
    app.run(debug=True, port=8090)
