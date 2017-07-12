//console.log("hiiiiiii I am a seal bark!");
var r = React.createElement;
var outerClass = {class:"col-lg-12 text-center"};
var innerClass = {class:"text-muted"};
var wallOfText = "Twitch.tv is a website where streamers live stream themselves providing content centered around their lives and video games. There are major facets of this experience that we display in the following sections: User, Game, Community, Team. A streamer(user) plays different games, takes part in different established communities centered around these games, and often join various esports teams which their streams then represent. Included with all of them are many other media and information which enhances each of those models. Twitch contains most of this information but we wanted to bring this information together in an easy to navigate environment.  We have named our website StreamGlean.me (glean - extract (information) from various sources) to represent the process of gathering stream information and sharing it with you guys."
ReactDOM.render(
	r('div', outerClass, null,
		r('small', innerClass, wallOfText)), document.getElementById('aboutText'));

// var searchNames = ['Sydney', 'Melbourne', 'Brisbane', 
//     'Adelaide', 'Perth', 'Hobart'];
// //...
// <DropdownInput 
//     options={searchNames}
//     defaultValue={this.props.initialValue}
//     menuClassName='dropdown-input'
//     onSelect={this.handleSelectName}
//     placeholder='Search...'
// />

