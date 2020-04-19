class Results {
  constructor() {
    const vw = Math.max(document.documentElement.clientWidth, window.innerWidth || 0)
    const vh = Math.max(document.documentElement.clientHeight, window.innerHeight || 0)

    this.svgWidth = (vw - 16) * 0.5
    this.svgHeight = vh - 200

    this.rankWidth = this.svgWidth * 0.07
    this.movieTitleWidth = this.svgWidth * 0.40

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
      let rank = {
        value: d.Rank,
        type: "rank"
      }
      let movieTitle = {
        value: d.Title,
        type: "title"
      }
      return [rank, movieTitle]
    })

    let newTd = td.enter()
      .append('td')

    td.exit()
      .remove()

    td = newTd.merge(td)

    let movieTitleCols = td.filter((d) => {
      return d.type === "title"
    })

    movieTitleCols
      .classed('movieTitles', true)
      .style('width', this.movieTitleWidth + 'px')

    td
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

}