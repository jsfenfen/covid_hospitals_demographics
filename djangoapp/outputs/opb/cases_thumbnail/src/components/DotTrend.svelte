<script>
	import { getContext } from 'svelte';
	const { data, xGet, yGet } = getContext('LayerCake');
	export let colorScale = d => '#000';
	//console.log("Dot trend with data");
	//console.log($data);

	$: path = values => {
		return 'M' + values
			.map(d => {
				return $xGet(d) + ',' + $yGet(d);
			})
			.join('L');
	};




	const fill = '#adb642';
	const stroke = '#333333';
	const r = 4;


	for (var i=0; i<$data[0]['values'].length; i++) {
		var this_x = $xGet($data[0]['values'][i]);
	}

</script>



<g class="scatter-group">
	{#each $data[0]['values'] as d}
		<circle
			cx={$xGet(d)}
			cy={$yGet(d)}
			{r}
			{fill}
		/>
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
