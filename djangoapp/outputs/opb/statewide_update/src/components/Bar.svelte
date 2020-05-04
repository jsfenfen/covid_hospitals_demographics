<script>
	import { getContext } from 'svelte';



	const { data, xGet, yGet, xScale, yScale } = getContext('LayerCake');

	export let colorScale = ["#00bbff","#00bbff","#00bbff"]

</script>

<g class="bar-group">
	{#each $data as d, i}
		<rect
			class='group-rect'
			data-id="{i}"
			x="{$xScale.range()[0]}"
			y="{$yGet(d)}"
			height={$yScale.bandwidth()}
			width="{$xGet(d)}"
			fill="{colorScale[i]}"
		></rect>
	{/each}
</g>




