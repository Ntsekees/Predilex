
const FIELDS_USING_IDS = [
	"id", "possible etymologies", "homoeventives", "similar",
	"antonyms", "hypernyms", "hyponyms", "holonyms", "meronyms",
	"related", "alt", "definition"
];

var g_keys = [];
var g_cols = [];
var g_data = [];
var g_selection = "All";
//var g_last_selected_row = null;

function highlight_row(row) {
	var t = row.constructor.name;
	console.assert(
		t === "HTMLTableRowElement",
		"⟦row⟧ is not an HTMLTableRowElement but a " + t + "!");
	// Remove highlight from previously selected row, if any
	const previously_selected_row =
		document.querySelector('tr.selected');
	if (previously_selected_row) {
		previously_selected_row.classList.remove('selected');
	}
	// Highlight the clicked row
	row.classList.add('selected');
	// g_last_selected_row = row;
}

function shift_selected_row(n) {
	const previously_selected_row =
		document.querySelector('tr.selected');
	if (previously_selected_row) {
		const newly_selected_row = (n > 0)
			? previously_selected_row.previousElementSibling
			: previously_selected_row.nextElementSibling;
		if (newly_selected_row) {
			highlight_row(newly_selected_row);
			update_details(newly_selected_row);
		}
	}
}

function handle_keydown(e) {
	e = e || window.event;
	if (e.keyCode == "38") {
		shift_selected_row(1);
	} else if (e.keyCode == "40") {
		shift_selected_row(-1);
	}
}

function hget(row, col_id) {
	if (row === null || row === undefined) return "";
	var i = g_keys.indexOf(col_id);
	if (i < 0) {
		console.log("⚠ ⟦hget⟧: column ⟪"+col_id+"⟫ does not exist!");
		return "";
	} else return row[i];
}

function parsed_filter(filter) {
	var split_filter = filter
		.replace("\\@", "\u0091")
		.split("@")
		.map((f) => f.replace("\u0091", "@"));
	var col_filters = split_filter.slice(1);
	var map = {};
	map.any = split_filter[0].trim();
	col_filters.forEach((f) => {
		f = f + " ";
		var i = f.indexOf(" ");
		map[f.slice(0, i).trim()] = new RegExp(f.slice(i).trim());
	});
	return map;
}

function validated_by_filter(entry, filter) {
	var pf = parsed_filter(filter);
	var found = false;
	for (k in pf) {
		if (k === "") return;
		if (k === "any") {
			if (pf[k] === "") found = true;
			else {
				g_keys.forEach((gk) => {
					if (hget(entry, gk).search(pf[k]) >= 0) {
						found = true;
					}
				});
			}
		} else {
			if (pf[k] === "") {
				if (hget(entry, k) === "")
					found = true;
			} else {
				if (hget(entry, k).search(pf[k]) >= 0)
					found = true;
			}
		}
		if (!found)
			return false;
		found = false;
	}
	return true;
}

function switch_display_to_all_fields() {
	document.getElementById("details-div").style.display = "flex";
	document.getElementById("col3-div").style.display = "none";
	document.getElementById("eng-div").className = "eng-td";
	document.getElementById("id-div").className = "id-td";
}

function switch_display_to_single_field() {
	document.getElementById("details-div").style.display = "none";
	document.getElementById("col3-div").style.display = "";
	document.getElementById("col3-div").innerHTML = g_selection;
	document.getElementById("eng-div").className = "eng2-td";
	document.getElementById("id-div").className = "id2-td";
}

function entry_from_id(id) {
	return g_data.find((row) => hget(row, "id") === id);
}

function go_to_id(id) {
	document.getElementById("filter-text").value =
		`@id ${id}`;
	run();
}

function interactivized_id(id) {
	return `
		<div class="details-popup">
			<b style="color: #003333; cursor: pointer;" onclick="go_to_id('${id}');">${id}</b>
			<span class="details-popup-text">
				${hget(entry_from_id(id), "eng_def")}
			</span>
		</div>
	`;
}

function with_interactive_ids(s) {
	return s.replace(
		/(?<![a-z])([bcdfghjklmnpqrstvwyz][aeiou]){3}(?![a-z])/g,
		(match) => interactivized_id(match));
}

function fmt(s) {
	if (s.includes("\n")) {
		var c = "";
		s.split("\n").forEach((e, i, l) => {
			c += "<tr><td>" + e + "</td></tr>";
		});
		s = "<table>" + c + "</table>";
	}
	return s;
}

function update_details(row) {
	var content = "";
	if (row.childElementCount > 0) {
		var first_id = "";
		for (const child of row.children) {
			first_id = child.innerText;
			break;
		}
		var entry = entry_from_id(first_id);
		g_keys.forEach((key) => {
			if (key) {
				var val = fmt(hget(entry, key));
				if (FIELDS_USING_IDS.includes(key))
					val = with_interactive_ids(val);
				if (g_selection != "AllNonempty" || val != "") {
					content += `
							<tr>
								<td class="field-td">
									${hget(g_cols, key)}
								</td>
								<td class="value-td">
									${val}
								</td>
							</tr>
					`;
				}
			}
		});
	}
	document.getElementById("details-body").innerHTML = content;
}

function run() {
	var prev_selection = g_selection;
	g_selection = document.getElementById("fields-selector").value;
	if (g_selection != prev_selection) {
		if (!["All", "AllNonempty"].includes(g_selection))
			switch_display_to_single_field();
		else switch_display_to_all_fields();
		//if (g_last_selected_row) update_details(g_last_selected_row);
	}
	var filter = document.getElementById("filter-text").value;
	var content = "";
	var count = 0;
	for (const row of g_data) {
		if (filter != "" && !validated_by_filter(row, filter)) continue;
		count += 1;
		var ext = "";
		var t = "";
		if (!["All", "AllNonempty"].includes(g_selection)) {
			t = "2";
			var val = fmt(hget(row, g_selection));
			if (FIELDS_USING_IDS.includes(g_selection))
				val = with_interactive_ids(val);
			ext = `
							<td class="col3-td">
								${val}
							</td>
			`
		}
		content += `
						<tr pred-id=${hget(row, "id")}>
							<td class="id${t}-td">
								${hget(row, "id")}
							</td>
							<td class="eng${t}-td">
								${hget(row, "eng_def")}
							</td>${ext}
						</tr>
		`;
	}
	document.getElementById("result-count").innerHTML = "(" + count + " results)";
	document.getElementById("entries-body").innerHTML = content;
	const rows = document.querySelectorAll('.entries tr');
	for (let i = 0; i < rows.length; i++) {
		let row = rows[i];

		row.onclick = function() {
			highlight_row(this);
			update_details(this);
			window.location.hash = `#${this.getAttribute('pred-id')}`;
		};

		if (window.location.hash === `#${row.getAttribute("pred-id")}`) {
			row.click();
			row.scrollIntoView({ behavior: "smooth", block: "center" });
		}
	}
}

function setup_2(data) {
	g_keys = data[0];
	g_cols = data[1];
	g_data = data.slice(2).filter((row) => hget(row, "eng_def") !== "");
	var s = "";
	g_keys.forEach((k) => {
		s += `<option value='${k}'>${k}</option>`;
	});
	document.getElementById("fields-selector").innerHTML += s;
	document.addEventListener('keydown', handle_keydown, true);
	const filter_text_input = document.getElementById('filter-text');
	filter_text_input.addEventListener('keydown', (event) => {
		if (event.key === 'Enter')
			run();
	});
	run();
}

function setup() {
	fetch('../predilex.csv')
    .then((response) => response.text())
    .then((csv) => {setup_2($.csv.toArrays(csv))});
}

setup();

