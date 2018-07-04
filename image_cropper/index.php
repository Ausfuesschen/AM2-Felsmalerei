<?php
	if (isset($_POST['submit'])) {
		$category = $_POST["category"];
		$url = $_POST["url"];
		$image = file_get_contents($url);
		file_put_contents('images/' . $category . '/img.png', $image);
	}
?>

<html>
	<head lang="en">
		<meta charset="UTF-8">
		<title>Image Cropper</title>
	</head>
		<div>
			Select image to crop: <input type="file" id="fileInput" name="file" multiple="" />
		</div>
		<div>
			<form method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>">
				<div >Image URL: <input id="imgurl" type="text" name="url" value="" readonly /></div>
				Category:
				<input type="radio" name="category" value="man" required />Man
				<input type="radio" name="category" value="woman" required >Woman
				<input type="radio" name="category" value="animal" required />Animal
				<input type="radio" name="category" value="text" required />Text
				<input type="submit" name="submit" value="Save" />
			</form>
		</div>
		<div>
			<canvas id="imageCanvas" width="1200" height="700" style="border:0px solid #000000;">
			</canvas>
		</div>
		<br>
		<div>
		Cropped image:
		</div>
		<div id="preview"></div>
		<script src="js/script.js"></script>
		<script src="js/ImageCropper.js"></script>
	</body>
</html>
