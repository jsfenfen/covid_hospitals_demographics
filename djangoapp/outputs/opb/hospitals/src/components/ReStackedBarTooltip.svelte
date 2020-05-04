<script>
  import { getContext } from 'svelte';

  import QuadTree from './QuadTree.svelte';

  const { height, width, yScale, originalSettings, data, yGet } = getContext('LayerCake');

  export let dataset;

  const w = 150;
  let top = 0;
  let bar_bottom = $height;

  $: columnHeight = d => {
    console.log("col height " + $height + " $yGet(d) " + $yGet(d));
    return $height - $yGet(d);
  };

  const columnWidth = (1/2)*$width / $data[0]['values'].length;

  console.log("DTTT columnWidth " + columnWidth);

  const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

  function capitalize (str) {
    return str.charAt(0).toUpperCase() + str.slice(1, str.length);
  }

  function addCommas (num) {
    const parts = String(num).split('.');
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return parts.join('.');
  }

  let contents = '';

  function setContents (result) {
    if (Object.keys(result).length === 0) return '';
    const rows = Object.keys(result).filter(d => d !== $originalSettings.x).map(key => {

      var valtoshow = result[key];
      if (valtoshow == '0') {
        valtoshow = 'NA';
      }
      return {
        key,
        value: valtoshow
      };
    })

    //.sort((a, b) => b.value - a.value);

    top = $yScale(rows[2].value);

    var display_rows = [rows[0], rows[1], rows[2]];

    return `
      <div style="font-weight: bold;">${monthNames[result[$originalSettings.x].getUTCMonth()]} ${result[$originalSettings.x].getUTCDate()}</div>
      ${display_rows.map(row => `<div><span style="color: #999; width: 65px;display:inline-block;">${capitalize(row.key)}:</span> ${addCommas(row.value)}</div>`).join('')}`;
  }

  function shouldbe_visible(visible) {
    console.log(visible);
    return visible ? 'block' : 'none' 

  }
</script>

<style>
  .tooltip {
    position: absolute;
    font-size: 13px;
    pointer-events: none;
    border: 1px solid #ccc;
    background: rgba(255, 255, 255, 0.95);
    transform: translate(-50%, -100%);
    padding: 5px;
    transition: left 250ms ease-out, top 250ms ease-out;
    z-index: 15;
  }

.fauxbar {
    position: absolute;
    background-color: transparent;
    pointer-events: none;
    border: 2px solid black;
  }
</style>

<QuadTree
  {dataset}
  y='x'
  let:x
  let:y
  let:visible
  let:found
  let:e
>

  <div class="tooltip"
    style="width:{w}px;display: { visible ? 'block' : 'none' };top:{top-20}px;left:{Math.min(Math.max(w, x), $width - w)}px;">{@html setContents(found)}</div>


      <div class="fauxbar"
          style="top:{top}px;left:{x-columnWidth/2}px; width:{columnWidth}px; height:{$height-top}px; display: { shouldbe_visible(visible)};"
      ></div>

</QuadTree>

