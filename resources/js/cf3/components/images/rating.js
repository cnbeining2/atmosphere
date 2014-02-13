define(['react'], function(React) {
    var Rating = React.createClass({
        render: function() {
            var repeatString = function(string, num) {
                return new Array( num + 1 ).join( string );
            };
            return React.DOM.div({className: 'star-rating'}, 
                repeatString("\u2605", this.props.rating) + 
                repeatString("\u2606", 5 - this.props.rating));
        }
    });

    return Rating;
});
