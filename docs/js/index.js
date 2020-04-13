// Search bar events
function search_request() {
  let query_text = $("#search_bar_input").val()
  if (query_text != "") {
    console.log(query_text)
  }
}

$("#search_bar_input").on("keyup", function (event) {
  if (event.keyCode === 13) {
    event.preventDefault()
    search_request()
  }
})