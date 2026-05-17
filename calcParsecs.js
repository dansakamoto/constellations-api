const starName = "β Lib";

const rightAscension = "15 17 00.41382";
const declination = "-09 22 58.4919";

const parallax_in_milliarcseconds = 17.62;
const parallax_in_arcseconds = parallax_in_milliarcseconds / 1000;

const parsecs = 1 / parallax_in_arcseconds;

const lightYears = parsecs * 3.26156;

console.log(
  `Star: ${starName}\nX-Axis: ${rightAscension}\nY-Axis: ${declination}\nDistance in parsecs: ${parsecs}\nDistance in light years: ${lightYears}`,
);
