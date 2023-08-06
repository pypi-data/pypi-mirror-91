from datetime import datetime
from typing import Any, Dict, Optional

import orm

from aopi_python.ctx import context
from aopi_python.models.dist_info import DistInfoModel
from aopi_python.models.pythonpackage import PythonPackage


class PythonPackageVersion(orm.Model):
    __tablename__ = "python_packages_versions"
    __database__ = context.database
    __metadata__ = context.metadata

    id = orm.Integer(primary_key=True)
    package = orm.ForeignKey(PythonPackage)
    user_id = orm.Integer(index=True, allow_null=True)

    size = orm.Integer()
    version = orm.Text()
    requires_python = orm.Text()
    yanked = orm.Boolean(default=False)
    comment_text = orm.Text(allow_null=True)
    yanked_reason = orm.Text(allow_null=True)
    filetype = orm.String(max_length=30)
    metadata_version = orm.Float()
    downloads = orm.Integer(default=0)
    filename = orm.Text(allow_null=False)
    md5_digest = orm.Text(allow_null=True)
    description = orm.Text(allow_null=True)
    sha256_digest = orm.Text(allow_null=True)
    upload_time = orm.DateTime(default=datetime.now)
    requires_dist = orm.Text(allow_null=True)
    description_content_type = orm.Text(allow_null=True)
    python_version = orm.Text(allow_null=True)

    @staticmethod
    def cast_upload_to_dict(filename: str, upload: DistInfoModel) -> Dict[str, Any]:
        return dict(
            version=upload.version,
            description=upload.description,
            comment_text=upload.comment,
            filetype=upload.filetype,
            metadata_version=upload.metadata_version,
            filename=filename,
            md5_digest=upload.md5_digest,
            requires_python=upload.requires_python,
            sha256_digest=upload.sha256_digest,
            description_content_type=upload.description_content_type.value
            if upload.description_content_type
            else None,
            requires_dist=";".join(upload.requires_dist)
            if upload.requires_dist
            else None,
            python_version=upload.python_version,
        )

    @classmethod
    async def create_by_dist_info(
        cls,
        *,
        filename: str,
        package: PythonPackage,
        size: int,
        dist_info: DistInfoModel,
        user_id: Optional[int]
    ) -> "PythonPackageVersion":
        info_dict = cls.cast_upload_to_dict(filename, dist_info)
        return await cls.objects.create(
            package=package, size=size, user_id=user_id, **info_dict
        )

    async def update_by_dist_info(
        self,
        *,
        filename: str,
        package: PythonPackage,
        size: int,
        dist_info: DistInfoModel
    ) -> "PythonPackageVersion":
        info_dict = self.cast_upload_to_dict(filename, dist_info)
        return await self.update(package=package, size=size, **info_dict)
