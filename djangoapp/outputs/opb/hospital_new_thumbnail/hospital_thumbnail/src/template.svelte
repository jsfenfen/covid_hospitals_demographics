<script>
	export let head = '';
	export let html = '';
	export let includeJS = true;

	const version = Date.now();
</script>

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset='utf-8'>
	<meta name='viewport' content='width=device-width,initial-scale=1'>

	<title>Oregon Hospitalizations</title>

	<link rel='icon' type='image/png' href='favicon.png'>

	<link rel="preconnect" href="https://fonts.gstatic.com">
	<link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@500&family=Roboto:wght@400;700&display=swap" rel="stylesheet"> 
	<script src="https://pym.nprapps.org/pym.v1.min.js" type="text/javascript"></script>


	<link rel='stylesheet' href='global.css'>
	<link rel='stylesheet' href='build/bundle.css?version={version}'>


	{@html head}
</head>

<body style="font-family: 'Roboto'; height: 200px; padding: 0px; margin: 0px; font-weight: 400; color: #36362b; overflow:hidden;">


  	<script defer src='build/bundle.js?version={version}'></script>


	{@html html}
</body>
</html>
