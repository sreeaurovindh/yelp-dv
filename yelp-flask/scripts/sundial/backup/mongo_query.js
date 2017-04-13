db.foodbusiness.aggregate(
	// Pipeline
	[
		// Stage 1
		{
			$group: {
			    '_id': {
			        'state': '$state',
			        'city': '$city',
			    },
			    postals: { $addToSet: { postal: "$postal_code", categories:"$categories" } } 
			}
		},

		// Stage 2
		{
			$group: {
			    '_id': {
			        'state': '$_id.state'
			    },
			    cities: { $addToSet: { city: "$_id.city", postals:"$postals" } }
			}
		},
	]
);
