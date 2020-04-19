class Results {
  constructor() {
    const vw = Math.max(document.documentElement.clientWidth, window.innerWidth || 0)
    const vh = Math.max(document.documentElement.clientHeight, window.innerHeight || 0)

    this.svgWidth = (vw - 16) * 0.7
    this.svgHeight = vh - 200

    this.rankWidth = this.svgWidth * 0.04
    this.movieTitleWidth = this.svgWidth * 0.25
    this.actorsWidth = this.svgWidth * 0.58
    this.yearWidth = this.svgWidth * 0.06
    this.avgVoteWidth = this.svgWidth * 0.07

    this.toggleSort = true

    this.data = null
  }


  setupView() {
    // this.svg = d3.select("#results").append('svg')
    //   .attr('width', this.svgWidth)
    //   .attr('height', this.svgHeight)

    d3.select('#rankHeader')
      .style('width', this.rankWidth + 'px')

    d3.select('#movieTitleHeader')
      .style('width', this.movieTitleWidth + 'px')

    d3.select('#actorsHeader')
      .style('width', this.actorsWidth + 'px')

    d3.select('#yearHeader')
      .style('width', this.yearWidth + 'px')

    d3.select('#avgVoteHeader')
      .style('width', this.avgVoteWidth + 'px')

    let that = this;

    // For sorting the list.
    d3.select('thead').selectAll('th')
      .on('click', function () {
        if (that.data === null) {
          return
        }
        that.collapseList()
        if (this.textContent.includes('Movie Title')) {
          if (that.toggleSort) {
            that.sortAscending('Title')
          } else {
            that.sortDescending('Title')
          }
        }
        if (this.textContent.includes('Rank')) {
          if (that.toggleSort) {
            that.sortAscending('Rank')
          } else {
            that.sortDescending('Rank')
          }
        }
        if (this.textContent.includes('Year')) {
          if (that.toggleSort) {
            that.sortAscending('Year')
          } else {
            that.sortDescending('Year')
          }
        }
        if (this.textContent.includes('Avg. Vote')) {
          if (that.toggleSort) {
            that.sortAscending('Avg Vote')
          } else {
            that.sortDescending('Avg Vote')
          }
        }
        that.toggleSort = !that.toggleSort
        that.updateTable()
      })
  }

  updateTable() {

    let that = this

    // Create table rows based on all the data
    let tr = d3.select("#resultsTBody").selectAll('tr').data(this.data)

    let newTr = tr.enter()
      .append('tr')
      .on('click', function () {
        let selectedMovie = this
        if (selectedMovie.__data__.ID !== "expanded") {
          that.insertToList(selectedMovie.rowIndex - 1)
        }
      })

    tr.exit()
      .remove()

    tr = newTr.merge(tr)

    tr.attr('id', (d) => {
      return `${d.ID}Row`
    })

    tr
      .classed('border_bottm', true)

    // Create table columns
    let td = tr.selectAll('td').data((d) => {
      if (d.ID === "expanded") {
        d.type = d.ID
        d.field = d.ID
        return [d]
      }
      let rank = {
        value: d.Rank,
        field: "rank",
        type: "text"
      }
      let movieTitle = {
        value: d.Title,
        field: "title",
        type: "text"
      }
      let actors = {
        value: d.Actors,
        field: "actors",
        type: "text"
      }
      let year = {
        value: parseInt(d.Year),
        field: "year",
        type: "text"
      }
      let avgVote = {
        value: parseFloat(d['Avg Vote']),
        field: "avgVote",
        type: "text"
      }
      return [rank, movieTitle, actors, year, avgVote]
    })

    let newTd = td.enter()
      .append('td')

    td.exit()
      .remove()

    td = newTd.merge(td)

    // Reset the colspan back to 1 and the background color
    td
      .attr('colspan', 1)
      .classed('no_padding', false)

    let expandedCol = td.filter((d) => {
      return d.type === "expanded"
    })

    // Set the expanded col to span all columns
    expandedCol
      .attr('colspan', 5)
      .classed('no_padding', true)

    expandedCol
      .html((d) => {
        return this.movieMoreInfoRender(d)
      })

    let movieTitleCols = td.filter((d) => {
      return d.field === "title"
    })

    movieTitleCols
      .classed('movieTitles', true)
      .style('width', this.movieTitleWidth + 'px')

    let textCols = td.filter((d) => {
      return d.type === "text"
    })

    textCols
      .text(d => d.value)
  }

  updateList(data) {
    this.data = data
  }

  insertToList(i) {
    let updatedData = []
    for (let j = 0; j < this.data.length; j++) {
      updatedData.push(this.data[j])
      if (i === j) {
        while (this.data[j + 1] && this.data[j + 1].ID === "expanded") {
          j += 1
        }
      }
      if (i === j) {
        let toInsert = Object.assign({}, this.data[i])
        toInsert.ID = "expanded"
        toInsert.id = this.data[i].ID
        updatedData.push(toInsert)
      }
    }
    this.data = updatedData
    this.updateTable()
  }

  collapseList() {
    let updatedData = []
    this.data.forEach((d, i) => {
      if (d.ID !== "expanded") {
        updatedData.push(d)
      }
    })
    this.data = updatedData
  }

  /**
   * Sorts the data list by ascending oder.
   * @param key - Key to sort by
   */
  sortAscending(key) {
    this.data.sort(function (x, y) {
      return d3.ascending(x[key], y[key]);
    });
  }

  /**
   * Sorts the data list in descending order.
   * @param key - Key to sort by
   */
  sortDescending(key) {
    this.data.sort(function (x, y) {
      return d3.descending(x[key], y[key]);
    });
  }

  movieMoreInfoRender(d) {
    let htmlRender = `<div class="flex_column expanded">
      <div class="flex_row">
      <div class="flex_row metaData">
      <div>
      <p><b>Director:</b> ${d.Director}</p>
      <p><b>Writer:</b> ${d.Writer}</p>
      <p><b>Country:</b> ${d.Country}</p>
      <p><b>Genre:</b> ${d.Genre}</p>
      <p><b>Duration:</b> ${d.Duration}</p>
      </div>
      <div>
      <p><b>Date Published:</b> ${d['Date Published']}</p>
      <p><b>Language:</b> ${d.Language}</p>`

    if (d['Production Company'] !== "") {
      htmlRender += `<p><b>Production</b> Company: ${d['Production Company']}</p>`
    }
    if (d['USA Gross Income'] !== "") {
      htmlRender += `<p><b>USA Gross Income:</b> ${d['USA Gross Income']}</p>`
    }
    if (d['Worldwide Gross Income'] !== "") {
      htmlRender += `<p><b>Worldwide Gross Income:</b> ${d['Worldwide Gross Income']}</p>`
    }

    htmlRender += `</div></div><div class="description"><b>Description:</b>`

    if (d.Description !== "") {
      htmlRender += `<p>${d.Description}</p>`
    }

    htmlRender += `</div>
      </div>
      <div class="flex_row reviews">
        <div>`

    if (d['Reviews From Critics'] !== "") {
      htmlRender += `<p><b>Reviews From Users:</b> ${parseInt(d['Reviews From Critics'])}</p>`
    }
    if (d['Reviews From Users'] !== "") {
      htmlRender += `<p><b>Reviews From Critics:</b> ${parseInt(d['Reviews From Users'])}</p>`
    }
    if (d.Reviews.length !== 0) {
      htmlRender += `<button class="reviewsButton" onclick="reviewButtonClick(${d.id})">Reviews</button>`
    }
    htmlRender += `</div></div></div>`
    return htmlRender
  }
}