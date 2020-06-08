<script>
	import { getContext } from 'svelte';
	const { data, xGet, yGet, height, width } = getContext('LayerCake');
	export let colorScale = d => '#000';
	console.log("Restacked bar with data");

	console.log("1");

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

	const fill2 = '#b2bc00';
	const fill1 = '#6d6d00';
	const stroke = '#333333';
	const strokeWidth = 1;
	const barstroke1 = '#cccccc';
	const barstroke2 = '#cccccc';

	const r = 4;


</script>


<g class="column-group">
	{#each $data[2]['values'] as d, i}
		<rect
			class='group-rect'
			data-id="{i}"
			x="{$xGet(d)-columnWidth/2}"
			y="{$yGet(d)}"
			width="{columnWidth}"
			height="{columnHeight(d)}"
			fill="{fill2}"
			stroke="{barstroke1}"
			stroke-width="{strokeWidth}"
		></rect>
	{/each}
</g>


<g class="column-group">
	{#each $data[1]['values'] as d, i}
		<rect
			class='group-rect'
			data-id="{i}"
			x="{$xGet(d)-columnWidth/2}"
			y="{$yGet(d)}"
			width="{columnWidth}"
			height="{columnHeight(d)}"
			fill="{fill1}"
			stroke="{barstroke2}"
			stroke-width="{strokeWidth}"
		></rect>
	{/each}
</g>










<style>
	.path-line {
		fill: none;
		stroke-linejoin: round;
		stroke-linecap: round;
		stroke-width: 3px;
	}
</style>
