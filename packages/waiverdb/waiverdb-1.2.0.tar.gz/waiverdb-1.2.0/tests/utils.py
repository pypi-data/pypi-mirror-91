# SPDX-License-Identifier: GPL-2.0+

from waiverdb.models import Waiver


def create_waiver(session, subject_type, subject_identifier, testcase, username, product_version,
                  waived=True, comment=None, proxied_by=None, scenario=None):
    waiver = Waiver(subject_type, subject_identifier, testcase, username, product_version,
                    waived, comment, proxied_by, scenario)
    session.add(waiver)
    session.flush()
    return waiver
