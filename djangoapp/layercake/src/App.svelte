<script>
  import { LayerCake, Svg, Html } from 'layercake';
  import { scaleOrdinal } from 'd3-scale';
  import { scaleLog } from 'd3-scale';
  import data from './data/testdata.js';
  import MultiLine from './components/MultiLine.svelte';
  import AxisX from './components/AxisX.svelte';
  import AxisY from './components/AxisY.svelte';
  import AxisYLog from './components/AxisYLog.svelte';
  import Labels from './components/Labels.svelte';
  import Tooltip from './components/Tooltip.svelte';
  import QuadTree from './components/QuadTree.svelte';


  /* --------------------------------------------
   * Set what is our x key to separate it from the other series
   */
  const xKey = 'month';

  const seriesNames = Object.keys(data[0]).filter(d => d !== xKey);
  const seriesColors = [
    '#ffe4b8',
    '#ffb3c0',
    '#ff7ac7',
    '#ff00cc'
  ];

  const dataLong = Object.keys(data[0]).map(key => {
    if (key === 'month') return null;
    return {
      key,
      values: data.map(d => {
        return { key, month: d[xKey], value: d[key] };
      })
    };
  }).filter(d => d);

  // Make a flat array of the `values` of our nested series
  // we can pluck the `value` field from each item in the array to measure extents
  const flatten = data => data.reduce((store, group) => store.concat(group.values), []);

  const monthNames = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.'];

  const colorScale = scaleOrdinal()
    .domain(seriesNames)
    .range(seriesColors);

  function formatTickX (d) {
  	console.log("formatTickX " + d);
    const date = new Date(d);
    var day = date.getDate();
    if (day%2==1) {
      return `${monthNames[date.getUTCMonth()]} ${date.getUTCDate()}`;
    } else {
      return '';
    }
  }
  
  function formatTickY (d) {
    if (d > 999) {
      return d / 1000 + 'k';
    }
    return d;
  }
  
</script>

<style>
  .chart-container {
    width: 100%;
    height: 100%;
  }
  .title {
  	margin-top: 20px;
  }
</style>
<div class="title">

<h2>Oregon COVID-19 confirmed cases and deaths, log scale</h2>
</div>
<div class="chart-container">
	
  <LayerCake
    padding={{ top: 27, right: 10, bottom: 20, left: 35 }}
    x='month'
    y='value'
    flatData={flatten(dataLong)}
    yDomain={[1, null]}
	yScale={scaleLog()}
    data={dataLong}
  >
    <Svg>
      <AxisX
        gridlines={false}
        ticks={data.map(d => d[xKey])}
        formatTick={formatTickX}
        snapTicks={true}
      />
      <AxisYLog
        formatTick={formatTickY}
      />

      <MultiLine
        {colorScale}
      />
    </Svg>

    <Html>
      <Labels/>
      <Tooltip
        dataset={ data }
      />
    </Html>
  </LayerCake>
</div>
<div class="title">
<h2>Oregon COVID-19 confirmed cases and deaths, linear scale</h2>
</div>
<div class="chart-container">
		

  <LayerCake
    padding={{ top: 27, right: 10, bottom: 20, left: 35 }}
    x='month'
    y='value'
    flatData={flatten(dataLong)}
    data={dataLong}
  >
    <Svg>
      <AxisX
        gridlines={false}
        ticks={data.map(d => d[xKey])}
        formatTick={formatTickX}
        snapTicks={true}
      />
      <AxisY
        formatTick={formatTickY}
      />

      <MultiLine
        {colorScale}
      />
    </Svg>

    <Html>
      <Labels/>
      <Tooltip
        dataset={ data }
      />
    </Html>
  </LayerCake>
</div>
