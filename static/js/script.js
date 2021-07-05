function toText(arr) {
    const recur = ({ Item, Children }) =>
        Item?.Name +
        (Children?.length
            ? "\n" +
              Children.map(recur)
                  .map((text, i, { length }) =>
                      i < length - 1
                          ? "├──" +
                            text.replace(
                                /\n/g,
                                "\n&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                            )
                          : "└──" +
                            text.replace(
                                /\n/g,
                                "\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                            )
                  )
                  .join("\n")
            : "");
    console.log(arr.map(recur).join("\n"));
    return arr.map(recur).join("\n");
}

$(document).ready(function () {
    $("form").on("submit", function (event) {
        word = $("#textInput").val();
        option = $("input:radio[name=searchOption]:checked").val();
        if (option !== "3") {
            recursive = option === "2" ? "True" : "False";
            $.ajax({
                type: "GET",
                url: `/origin/${word}?recursive=${recursive}`,
                dataType: "json",
            }).done(function (data) {
                if (data.length === 0) {
                    $("#results").html("<h2>No result found :(</h2>");
                } else {
                    results = `<h2>${data.length} origin words found for ${word}</h2>`;
                    results += `<ul style="list-style: none;">\n`;
                    data.forEach((datum) => {
                        results += `<li><u>${datum}</u></li>\n`;
                    });
                    results += "</ul>";
                    $("#results").html(results);
                }
            });
        } else {
            $.ajax({
                type: "GET",
                url: `/tree/${word}`,
                dataType: "json",
            }).done(function (data) {
                if (Object.keys(data).length === 0) {
                    $("#results").html("<h2>No result found :(</h2>");
                } else {
                    results = `<h2>Etymology Tree for ${word}</h2>`;
                    results += toText(data);
                    $("#results").html(results);
                }
            });
        }
        event.preventDefault();
    });
});
