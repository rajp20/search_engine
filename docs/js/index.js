// Search bar events
$("#search_bar_input").on("keyup", function (event) {
  if (event.keyCode === 13) {
    search_request()
  }
})

function handle_search_response(data) {
  console.log(data)
}

function search_request() {
  let query_text = $("#search_bar_input").val()
  if (query_text != "") {
    console.log('Making search request...')
    $.ajax({
      'type': 'GET',
      'url': "http://localhost:8000/search",
      'data': {
        'search_query': query_text
      },
      'success': handle_search_response
    })
  }
}