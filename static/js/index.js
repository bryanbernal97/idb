//console.log("hiiiiiii I am a seal bark!");
/**
  * @jsx React.DOM
*/

var r = React.createElement;
var outerClass = {class:"col-lg-12 text-center"};
var innerClass = {class:"text-muted"};
var wallOfText = "Twitch.tv is a website where streamers live stream themselves providing content centered around their lives and video games. There are major facets of this experience that we display in the following sections: User, Game, Community, Team. A streamer(user) plays different games, takes part in different established communities centered around these games, and often join various esports teams which their streams then represent. Included with all of them are many other media and information which enhances each of those models. Twitch contains most of this information but we wanted to bring this information together in an easy to navigate environment.  We have named our website StreamGlean.me (glean - extract (information) from various sources) to represent the process of gathering stream information and sharing it with you guys."
ReactDOM.render(
	r('div', outerClass, null,
		r('small', innerClass, wallOfText)), document.getElementById('aboutText'));

// var SearchBox = React.createClass({
//     doSearch:function(){
//         var query=this.refs.searchInput.getDOMNode().value; // this is the search text
//         this.props.doSearch(query);
//     },
//     render:function(){
//         return <input type="text" ref="search_string" placeholder="Search..." value={this.props.query} onChange={this.doSearch}/>
//     }
// });

// var InstantBox = React.createClass({
//     doSearch:function(queryText){
//         console.log(queryText)
//         //get query result
//         var queryResult=[];
//         this.props.data.forEach(function(person){
//             if(person.name.toLowerCase().indexOf(queryText)!=-1)
//             queryResult.push(person);
//         });
 
//         this.setState({
//             query:queryText,
//             filteredData: queryResult
//         })
//     },
//     getInitialState:function(){
//         return{
//             query:'',
//             filteredData: this.props.data
//         }
//     },
//     render:function(){
//         return (
//             <div className="InstantBox">
//                 <h2>Void Canvas Instant Search</h2>
//                 <SearchBox query={this.state.query} doSearch={this.doSearch}/>
//                 <DisplayTable data={this.state.filteredData}/>
//             </div>
//         );
//     }
//});