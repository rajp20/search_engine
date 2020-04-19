let resultsView = new Results()
resultsView.setupView()

let receivedData = null

// Search bar events
$("#search_bar_input").on("keyup", function (event) {
  if (event.keyCode === 13) {
    search_request()
  }
})

function handle_search_response(data) {
  console.log("Received list from server.")
  console.log(data)
  receivedData = data
  resultsView.updateList(Object.values(data))
  resultsView.sortAscending('Rank')
  resultsView.updateTable()
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
      'timeout': 300000,
      'success': handle_search_response
    })
  }
}

function reviewButtonClick(id) {
  if (receivedData === null) {
    return
  }
  let modelContent = document.getElementById('modal-content-id')
  let htmlToAdd = '<span id="close-id" class="close">&times;</span>'
  htmlToAdd += getReviewHTML(id)

  modelContent.innerHTML = htmlToAdd
  modal.style.display = "block";
  $('#close-id').click(function () {
    modal.style.display = "none";
  })
}

function getReviewHTML(id) {
  let reviews = receivedData[id].Reviews
  let htmlToAdd = ""
  reviews.forEach((rev) => {
    htmlToAdd += `<p><b>Reviewer Name:</b> ${rev.reviewerName}</p>`
    htmlToAdd += `<p><b>Reviewer ID:</b> ${rev.reviewerID}</p>`
    htmlToAdd += `<p><b>Summary:</b> ${rev.summary}</p>`
    htmlToAdd += `<p><b>Review Text:</b></p>`
    htmlToAdd += `<p>${rev.reviewText}</p>`
    htmlToAdd += `<p>---</p>`
  })
  return htmlToAdd
}

// Get the modal
let modal = document.getElementById("myModal");

// Get the button that opens the modal
let btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
let span = document.getElementsByClassName("close")[0];

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}