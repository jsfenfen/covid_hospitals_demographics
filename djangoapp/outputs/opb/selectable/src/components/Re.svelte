<script>
	import { getContext } from 'svelte';
	const { data, xGet, yGet, height, width } = getContext('LayerCake');
	export let colorScale = d => '#000';
	console.log("Dot trend with data");
	console.log($data);

	$: path = values => {
		return 'M' + values
			.map(d => {
				return $xGet(d) + ',' + $yGet(d);
			})
			.join('L');
	};

	$: columnHeight = d => {
		return $height - $yGet(d);
	};

	const columnWidth = $width / $data[0]['values'].length;

	console.log("columnWidth " + columnWidth);

	const fill = '#e09d1f';
	const stroke = '#333333';
	const strokeWidth = 1;
	const barstroke = '#cccccc';

	const r = 4;


</script>


<g class="column-group">
	{#each $data[0]['values'] as d, i}
		<rect
			class='group-rect'
			data-id="{i}"
			x="{$xGet(d)-columnWidth/2}"
			y="{$yGet(d)}"
			width="{columnWidth}"
			height="{columnHeight(d)}"
			{fill}
			stroke="{barstroke}"
			stroke-width="{strokeWidth}"
		></rect>
	{/each}
</g>


<g class="line-group">
		<path
			class='path-line'
			d='{path($data[1].values)}'
			stroke="{stroke}"
		></path>
</g>






<style>
	.path-line {
		fill: none;
		stroke-linejoin: round;
		stroke-linecap: round;
		stroke-width: 3px;
	}
</style>
