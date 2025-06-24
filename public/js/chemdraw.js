function renderSmiles() {
	const SmilesDrawer = window.SmilesDrawer;
	if (!SmilesDrawer) return;
	const options = { width: 100, height: 100 };
	const drawer = new SmilesDrawer.Drawer(options);

	document.querySelectorAll(".smiles").forEach((div) => {
		const smiles = div.textContent.trim();
		if (!smiles) return;
		div.innerHTML = "";
		SmilesDrawer.parse(
			smiles,
			(tree) => {
				const canvas = document.createElement("canvas");
				canvas.width = options.width;
				canvas.height = options.height;
				div.appendChild(canvas);
				drawer.draw(tree, canvas, "light", false);
			},
			(err) => {
				div.innerHTML = '<span style="color:red">SMILES Error</span>';
			},
		);
	});
}

document.addEventListener("DOMContentLoaded", renderSmiles);
document.addEventListener("swup:contentReplaced", () => {
	setTimeout(renderSmiles, 100);
});

let debounceTimer = null;
const observer = new MutationObserver(() => {
	if (debounceTimer) clearTimeout(debounceTimer);
	debounceTimer = setTimeout(renderSmiles, 50);
});
observer.observe(document.body, { childList: true, subtree: true });

window.renderSmiles = renderSmiles;
