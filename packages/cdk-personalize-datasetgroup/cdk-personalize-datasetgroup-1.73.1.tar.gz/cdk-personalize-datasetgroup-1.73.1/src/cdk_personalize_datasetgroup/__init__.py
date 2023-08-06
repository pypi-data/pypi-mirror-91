"""
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
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


class PersonalizeDatasetGroup(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-personalize-datasetgroup.PersonalizeDatasetGroup",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        dataset_group_name: typing.Optional[builtins.str] = None,
        interactions_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param dataset_group_name: The name for the Dataset Group. Default: - ``${id}-${STAGE}``
        :param interactions_schema: The schema to use for interactions. Default: - json string representing default interaction schema
        """
        props = PersonalizeDatasetGroupProps(
            dataset_group_name=dataset_group_name,
            interactions_schema=interactions_schema,
        )

        jsii.create(PersonalizeDatasetGroup, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="datasetGroupArn")
    def dataset_group_arn(self) -> builtins.str:
        return jsii.get(self, "datasetGroupArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="trackingArn")
    def tracking_arn(self) -> builtins.str:
        return jsii.get(self, "trackingArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="trackingID")
    def tracking_id(self) -> builtins.str:
        return jsii.get(self, "trackingID")


@jsii.data_type(
    jsii_type="cdk-personalize-datasetgroup.PersonalizeDatasetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_group_name": "datasetGroupName",
        "interactions_schema": "interactionsSchema",
    },
)
class PersonalizeDatasetGroupProps:
    def __init__(
        self,
        *,
        dataset_group_name: typing.Optional[builtins.str] = None,
        interactions_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param dataset_group_name: The name for the Dataset Group. Default: - ``${id}-${STAGE}``
        :param interactions_schema: The schema to use for interactions. Default: - json string representing default interaction schema
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if dataset_group_name is not None:
            self._values["dataset_group_name"] = dataset_group_name
        if interactions_schema is not None:
            self._values["interactions_schema"] = interactions_schema

    @builtins.property
    def dataset_group_name(self) -> typing.Optional[builtins.str]:
        """The name for the Dataset Group.

        :default: - ``${id}-${STAGE}``
        """
        result = self._values.get("dataset_group_name")
        return result

    @builtins.property
    def interactions_schema(self) -> typing.Optional[builtins.str]:
        """The schema to use for interactions.

        :default: - json string representing default interaction schema
        """
        result = self._values.get("interactions_schema")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PersonalizeDatasetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PersonalizeDatasetGroup",
    "PersonalizeDatasetGroupProps",
]

publication.publish()
