<script>
	import { getContext } from 'svelte';
	import * as geo from 'd3-geo';

	const { data, width, height } = getContext('LayerCake');

	export let projectionName = 'geoAlbersUsa';
	export let pointsData = [];
	
	$: projection = geo[projectionName]()
		.fitSize([$width, $height], $data);
</script>

<g class="points">
{#each pointsData as d} 
	<circle
		cx={projection(d['points'])[0]}
		cy={projection(d['points'])[1]}
		r="{d['prominence']}"
	>
	</circle>

	 <text x="{projection(d['points'])[0]+6}" y="{projection(d['points'])[1]+5}" class="{d['prominence'] == 3 ? 'small' : 'tiny' }">{d['name']}</text>
{/each}
</g>

<style>
	circle {
		fill: #000;
		stroke: #fff;
		stroke-width: 1;
	}
	.small { 
		font: italic 12px sans-serif;
	    paint-order: stroke;
	    fill: #333333;
	    stroke: #ffffff;
	    stroke-width: 2px;
	    stroke-linecap: butt;
	    stroke-linejoin: miter;
}
.tiny { 
		font: italic 10px sans-serif;
	    paint-order: stroke;
	    fill: #333333;
	    stroke: #ffffff;
	    stroke-width: 2px;
	    stroke-linecap: butt;
	    stroke-linejoin: miter;
}
</style>