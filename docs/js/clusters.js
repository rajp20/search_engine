class Clusters {
  constructor() {
    const vw = Math.max(document.documentElement.clientWidth, window.innerWidth || 0)
    const vh = Math.max(document.documentElement.clientHeight, window.innerHeight || 0)

    let svgWidth = (vw - 16)
    let svgHeight = vh - 200

    this.movieTitleWidth = svgWidth

    this.toggleSort = true

    this.data = {}
  }


  setupView() {
    // this.svg = d3.select("#results").append('svg')
    //   .attr('width', this.svgWidth)
    //   .attr('height', this.svgHeight)

    d3.selectAll('.movieTitleCluster')
      .style('width', this.movieTitleWidth + 'px')

    let that = this;

    // For sorting the list.
    d3.select('#clusters').selectAll('th')
      .on('click', function () {
        if (that.data === null) {
          return
        }
        if (this.textContent.includes('Movie Titles')) {
          let clusterIndex = parseInt(this.textContent[this.textContent.length - 1])
          console.log(clusterIndex)
          if (that.toggleSort) {
            that.sortAscending('Title', clusterIndex)
          } else {
            that.sortDescending('Title', clusterIndex)
          }
        }
        that.toggleSort = !that.toggleSort
        that.updateTable()
      })
  }

  updateTable() {
    let mostFreqTerms = []
    for (let i = 1; i <= 3; i++) {
      let freqTerms = this.data[i][0]['Frequent Terms']
      for (let item of freqTerms) {
        item = item.replace(',', '')
        if (!mostFreqTerms.includes(item)) {
          mostFreqTerms.push(item)
          let mostFreqID = `#cluster${i}FreqTerm`
          d3.select(mostFreqID)
            .html(`Most Freq Term for Cluster ${i}: <b>${item}</b>`)
          break
        }
      }

      let tableID = `#cluster${i}TBody`
      // Create table rows based on all the data
      let tr = d3.select(tableID).selectAll('tr').data(this.data[i])

      let newTr = tr.enter()
        .append('tr')

      tr.exit()
        .remove()

      tr = newTr.merge(tr)

      tr.attr('id', (d) => {
        return `${d.ID}ClusterRow`
      })

      tr
        .classed('border_bottm', true)

      // Create table columns
      let td = tr.selectAll('td').data((d) => {
        let movieTitle = {
          value: d.Title,
          field: "title",
          type: "text"
        }
        return [movieTitle]
      })

      let newTd = td.enter()
        .append('td')

      td.exit()
        .remove()

      td = newTd.merge(td)

      let movieTitleCols = td.filter((d) => {
        return d.field === "title"
      })

      movieTitleCols
        .style('width', this.movieTitleWidth + 'px')

      td
        .text(d => d.value)
    }
  }

  updateList(data) {
    this.data[1] = data.filter((d) => {
      return d.Cluster === 0
    })
    this.data[2] = data.filter((d) => {
      return d.Cluster === 1
    })
    this.data[3] = data.filter((d) => {
      return d.Cluster === 2
    })
  }

  /**
   * Sorts the data list by ascending oder.
   * @param key - Key to sort by
   */
  sortAscending(key, clusterIndex) {
    this.data[clusterIndex].sort(function (x, y) {
      return d3.ascending(x[key], y[key]);
    });
  }

  /**
   * Sorts the data list in descending order.
   * @param key - Key to sort by
   */
  sortDescending(key, clusterIndex) {
    this.data[clusterIndex].sort(function (x, y) {
      return d3.descending(x[key], y[key]);
    });
  }
}