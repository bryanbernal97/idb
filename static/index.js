console.log("hiiiiiii I am a seal bark!");
//var React = 'react';
//var ReactDOM = 'react-dom';
var blue = React.createElement;
var outerClass = {class:"col-lg-12 text-center"};
var innerClass = {class:"text-muted"};
var wallOfText = "Twitch.tv is a website where streamers live stream themselves providing content centered around their lives and video games. There are many facets of this experience that we define as models: User, Game, Community, Team. A streamer plays different games, takes part in different established communities centered around these games, and often join various esports teams which their streams then represent. Included with all of them are many other media and information which enhances each of those models. Twitch contains all of this information but there isn’t a good place that brings all of this information together in an easy to navigate environment. We decided to make this information more readily available by linking these data points together on a website.  We are accomplishing this by fleshing out different user use cases, scraping available RESTful API for Twitch and Giant Bomb and other supplementary data, defining important models which will connect to each other, and exploring new tools to make this process easier and more intuitive. We have named our website StreamGlean.me (glean - extract (information) from various sources) to represent the process of gathering stream information."
ReactDOM.render(
	blue('div', outerClass, null,
		blue('small', innerClass, wallOfText)), document.getElementById('root'));