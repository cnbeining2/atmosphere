define(['react', 'models/application', 'collections/applications',
    'components/images/rating'], function(React, App, AppCollection, Rating) {
    var ImageDetail = React.createClass({
        getInitialState: function() {
            return {image: null};
        },
        componentDidMount: function() {
            // TODO: This is what should happen if we have API support for it
            /*
            var app = new App({id: this.props.image_id});
            app.fetch({success: function(model) {
                this.setState({image: model});
            }.bind(this)});
            */
            // This is terrible.
            var apps = new AppCollection();
            apps.fetch({success: function(collection) {
                var app = collection.get(this.props.image_id);
                this.setState({image: app});
            }.bind(this)});
        },
        render: function() {
            var image = this.state.image;
            console.log(image);

            if (!image)
                return React.DOM.div({className: 'loading'});

            return React.DOM.div({}, 
                React.DOM.h1({}, image.get('name_or_id')),
                Rating({rating: image.get('rating')}),
                React.DOM.h2({}, "Description"),
                React.DOM.p({}, image.get('description')),
                React.DOM.h2({}, "Versions of this Image"));
        }
    });

    return ImageDetail;
});
