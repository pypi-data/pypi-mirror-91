# CDK Personalize DatasetGroup

## Resources Created

* Custom Resource Lambda Function
* Personalize Dataset Group
* Personalize Interactions Schema
* Personalize User-item interaction Dataset
* Personalize Event Tracker

## Returned Data

* Dataset Group Arn: `datasetGroupArn`
* Event Tracker Arn: `trackingArn`
* Event Tracker ID: `trackingID`

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk

personalize_dataset_group = PersonalizeDatasetGroup(self, "voxi-personalize",
    dataset_group_name="my-group-name", # Optional
    interactions_schema="{...}"
)

cdk.CfnOutput(self, "personalizeTrackingIDOutput",
    value=personalize_dataset_group.tracking_iD,
    description="Tracking ID Output for Amplify or something else"
)
```

## References

* [AWS Personalize](https://docs.aws.amazon.com/personalize/latest/dg/what-is-personalize.html)
* [Personalize SDK](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/Personalize.html)
* [Amplify Personalize](https://docs.amplify.aws/lib/analytics/personalize/q/platform/js)
