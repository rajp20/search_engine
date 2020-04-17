class Results {
  constructor() {
    const vw = Math.max(document.documentElement.clientWidth, window.innerWidth || 0)
    const vh = Math.max(document.documentElement.clientHeight, window.innerHeight || 0)

    this.svgWidth = (vw - 16) * 0.5
    this.svgHeight = vh - 16
  }

  setupView() {
    this.svg = d3.select("")
  }
}