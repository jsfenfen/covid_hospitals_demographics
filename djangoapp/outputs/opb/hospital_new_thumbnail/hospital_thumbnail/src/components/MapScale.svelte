<script>
  import { getContext } from 'svelte';

  const { data, xGet, yGet, height, xScale } = getContext('LayerCake');

  $: columnHeight = d => {
    return $height - $yGet(d);
  };

  /* --------------------------------------------
   * Default styles
   */
  export let fill = '#00e047';
  export let stroke = '#ffffff';
  export let strokeWidth = 0;
  export let colors = [];

</script>

<g class="column-group">
  {#each $data as d, i}
    <rect
      class='group-rect'
      data-id="{i}"
      x="{$xGet(d)+5}"
      y="{$yGet(d)}"
      width={$xScale.bandwidth()-5}
      height="{columnHeight(d)}"
      fill="{colors[i]}"
      stroke="{stroke}"
      stroke-width="{strokeWidth}"
    ></rect>
  {/each}
</g>